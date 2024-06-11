import requests


def place_order():
    token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik56WXpOekExUXpORVJFTXpNMFZHTkVSRVFqSTBSakV4TmpZek56aEdRVFJETmtJd1JVVXpNUSJ9.eyJodHRwOi8vdHJhZGVzdGF0aW9uLmNvbS9pZ25vcmVfZHVhbF9sb2dvbiI6ImZhbHNlIiwiaHR0cDovL3RyYWRlc3RhdGlvbi5jb20vY2xpZW50X3RhZyI6IlFsZzJsIiwiaHR0cDovL3RyYWRlc3RhdGlvbi5jb20vdXNlcm5hbWUiOiJhbGtodWxhaWZpYmludmVzdG1lbnQiLCJodHRwOi8vdHJhZGVzdGF0aW9uLmNvbS9mZGNuX2lkIjoiMTEwNzUxNDIiLCJodHRwOi8vdHJhZGVzdGF0aW9uLmNvbS9vbnl4X2lkIjo0NDE3NDE4LCJpc3MiOiJodHRwczovL3NpZ25pbi50cmFkZXN0YXRpb24uY29tLyIsInN1YiI6ImF1dGgwfDExMDc1MTQyIiwiYXVkIjpbImh0dHBzOi8vYXBpLnRyYWRlc3RhdGlvbi5jb20iLCJodHRwczovL3RyYWRlc3RhdGlvbi1wcm9kLnRzbG9naW4uYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTcxNzUyMzI4OCwiZXhwIjoxNzE3NTI0NDg4LCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIE1hcmtldERhdGEgUmVhZEFjY291bnQgVHJhZGUgb2ZmbGluZV9hY2Nlc3MiLCJhenAiOiJsTXVqRFRibUhycVo1YTdFa1BTeXNraXZZOWRvSHU1NCJ9.j0-aWnBr-gdSW5XWvu43Xb1igChj5nTJC24mU7v5dA7ZWafw4i43-VX2h01vpK10OCcHTIaiENd4Ch8n1aDWFn08tLi8PTMXdGQJtPBJTEdbDW7M-FFnaxfrdNXdwKiQv-2hJo5AD450JUfkxAauSKq9uZr78IKhVrtYSYem2Rw6SmMggBxE279RobEX8S6OInIHVnjOywv_w4-GfG1-fasGG0JVSqsUcZSd5GWC6forWjhrqEzkYo2boEmPwFBqM9P_IrfiOxJF2ktle1NkgP6pnzh8b3C4A_Rc1tby72mXZ6WedMSrjXy-YKa6WNjWSC2PvNHcWy7YFW3otM1nhw'

    url = "https://sim-api.tradestation.com/v3/orderexecution/orders"

    payload = {
        "AccountID": "SIM2731552M",
        "Symbol": "MSFT",
        "Quantity": "1",
        "OrderType": "Limit",
        "LimitPrice": "413.44",
        "StopPrice": "410.44",
        "TradeAction": "BUY",
        "TimeInForce": {
            "Duration": "DAY"
        },
        "Route": "Intelligent"
    }

    headers = {
        "content-type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    print(url)
    response = requests.request("POST", url, json=payload, headers=headers)

    print(response.text)



place_order()


def update_order(symbol, quantity, strategy_name):
    params = {
        "LimitPrice": "459.41",
        "StopPrice": "string",
        "OrderType": "string",
        "Quantity": "string",
        "Symbol": "string",
    }
"837131403"