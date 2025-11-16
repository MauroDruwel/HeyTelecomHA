from heytelecom import HeyTelecomClient

with HeyTelecomClient(email="", password="") as client:
    client.login()
    account_data = client.get_account_data()
    # Print provider information
    print(account_data.provider)

    # Print account details
    print(account_data.last_sync)

    # Print latest invoice details
    print(account_data.latest_invoice.amount_eur)
    print(account_data.latest_invoice.date)
    print(account_data.latest_invoice.due_date)
    print(account_data.latest_invoice.invoice_id)
    print(account_data.latest_invoice.paid)
    print(account_data.latest_invoice.status)

    # Print subscribed products
    for product in account_data.products:
        print(product.product_id)
        print(product.product_type)
        print(product.phone_number)
        print(product.tariff)
        print(product.contract.start_date)
        print(product.contract.price_per_month_eur)
        print(product.usage.period)
        print(product.usage.data)
        print(product.usage.calls)
        print(product.usage.sms_mms)
        print(product.easy_switch_number)