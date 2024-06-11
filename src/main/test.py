from src.core.ioc import container

tradestation_sdk = container.tradestation_sdk()


def main():
    client_id = 'lMujDTbmHrqZ5a7EkPSyskivY9doHu54'
    client_secret = 'AIK6Sot-Nz_QbwbOUuL5TuYZx741S978Jnie3pRQUt7PwusNBA4KdbcV8epUdRzg'
    code = 'authorization_code'
    redirect_uri = 'https://trading-platfrom.tw1.su/callback/'

    try:
        tokens = tradestation_sdk.exchange_code_to_tokens(
            client_id=client_id,
            client_secret=client_secret,
            code=code,
            redirect_uri=redirect_uri
        )
        print("Tokens received:", tokens)
    except Exception as e:
        print("Error occurred:", e)


if __name__ == "__main__":
    main()
