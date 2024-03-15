from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse
import db_helper
import generic_helper

app = FastAPI()

# To track ongoing Orders --------------
inprogress_orders = {}


@app.get("/")
async def root():
    print("Call The Get MEthod by Google dialog flow -----------  ")
    return {"message": "Hello World"}


@app.post("/")
async def handle_request(request: Request):
    print("Call The Post MEthod by Google dialog flow -----------  ")
    # Retrieve the JSON data from the request
    payload = await request.json()

    # Extract the necessary information from the payload
    # based on the structure of the WebhookRequest from Dialogflow
    intent = payload["queryResult"]["intent"]["displayName"]
    parameters = payload["queryResult"]["parameters"]
    output_contexts = payload["queryResult"]["outputContexts"]

    # Get session ID of the current dialogflow chat --------
    session_id = generic_helper.extract_session_id(output_contexts[0]["name"])

    intent_handler_dict = {
        "order.add - context: ongoing-order": add_to_order,
        "order.remove - context: ongoing-order": remove_from_order,
        "order.complete - context: ongoing-order": complete_order,
        "track.order - context: ongoing-tracking": track_order,
    }

    # if intent == "track.order - context: ongoing-tracking":
    #     # return JSONResponse(content={"fulfillmentText": f"Reccieved  === {intent}"})
    #     return track_order(parameters)

    return intent_handler_dict[intent](parameters, session_id)


def track_order(parameters: dict):
    order_id = int(parameters["number"])
    order_status = db_helper.get_order_status(order_id)
    if order_status:
        fulfillment_text = (
            f"The order status for order id: {order_id} is: {order_status}"
        )
    else:
        fulfillment_text = f"No order found with order id: {order_id}"

    return JSONResponse(content={"fulfillmentText": fulfillment_text})


def add_to_order(parameters: dict, session_id: str):
    food_items = parameters["food-item"]
    quantities = parameters["number"]

    if len(food_items) != len(quantities):
        fulfillment_text = "Sorry I didn't understand. Can you please specify food items and quantities clearly?"
    else:
        # merge the two lists into a dictionary (food-items and quantity)
        new_food_dict = dict(zip(food_items, quantities))

        # Update the inprogress_orders dictionary
        if session_id in inprogress_orders:
            # check existance by session id --------
            current_food_dict = inprogress_orders[session_id]
            current_food_dict.update(new_food_dict)
            inprogress_orders[session_id] = current_food_dict
        else:
            # add new order by session id  to dictionery  --------
            inprogress_orders[session_id] = new_food_dict

        print("****** inprogress_orders ************ ", inprogress_orders)
        # print session id
        print("****** session_id ************ ", session_id)

        order_str = generic_helper.get_str_from_food_dict(inprogress_orders[session_id])
        fulfillment_text = f"So far you have: {order_str}. Do you need anything else?"

    return JSONResponse(content={"fulfillmentText": fulfillment_text})


# Save to Order to DB
def save_to_db(order: dict):
    next_order_id = db_helper.get_next_order_id()

    # Insert individual items along with quantity in orders table
    for food_item, quantity in order.items():
        rcode = db_helper.insert_order_item(food_item, quantity, next_order_id)

        if rcode == -1:
            return -1

    # Now insert order tracking status
    db_helper.insert_order_tracking(next_order_id, "in progress")

    return next_order_id


def complete_order(parameters: dict, session_id: str):
    if session_id not in inprogress_orders:
        fulfillment_text = "I'm having a trouble finding your order. Sorry! Can you place a new order please?"
    else:
        order = inprogress_orders[session_id]
        order_id = save_to_db(order)
        if order_id == -1:
            fulfillment_text = (
                "Sorry, I couldn't process your order due to a backend error. "
                "Please place a new order again"
            )
        else:
            order_total = db_helper.get_total_order_price(order_id)

            fulfillment_text = (
                f"Awesome. We have placed your order. "
                f"Here is your order id # {order_id}. "
                f"Your order total is {order_total} which you can pay at the time of delivery!"
            )

        # Delete this session from my dictionery -------------------------
        del inprogress_orders[session_id]

    return JSONResponse(content={"fulfillmentText": fulfillment_text})


# remove add item from this list ------------------------------------------


def remove_from_order(parameters: dict, session_id: str):
    if session_id not in inprogress_orders:
        return JSONResponse(
            content={
                "fulfillmentText": "I'm having a trouble finding your order. Sorry! Can you place a new order please?"
            }
        )

    food_items = parameters["food-item"]
    current_order = inprogress_orders[session_id]

    removed_items = []
    no_such_items = []

    for item in food_items:
        if item not in current_order:
            no_such_items.append(item)
        else:
            removed_items.append(item)
            del current_order[item]

    if len(removed_items) > 0:
        fulfillment_text = f'Removed {",".join(removed_items)} from your order!'

    if len(no_such_items) > 0:
        fulfillment_text = (
            f' Your current order does not have {",".join(no_such_items)}'
        )

    if len(current_order.keys()) == 0:
        fulfillment_text += " Your order is empty!"
    else:
        order_str = generic_helper.get_str_from_food_dict(current_order)
        fulfillment_text += f" Here is what is left in your order: {order_str}"

    return JSONResponse(content={"fulfillmentText": fulfillment_text})