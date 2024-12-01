from pvz_client.api_auth import *
from pvz_client.api_client import *
import time


async def main():
    # auth_base_path = "https://r-point.wb.ru"
    # api_auth = ApiAuth(auth_base_path=auth_base_path, base_path=auth_base_path)
    # phone = "79282951709"
    # try:
    #     code_response = await api_auth.login(phone=phone)
    #     print("Code requested successfully:", code_response)
    # except HTTPException as e:
    #     print(f"Error requesting code: {e}")
    #     return
    #
    # code = input("Enter code received via SMS: ")
    # temp_token = code_response.data

    try:
        #token_response = await api_auth.validate(code=code, token=temp_token)
        #print("Connected successfully, tokens received:")
        #print(token_response.access.token)
        #access_token = token_response.access.token
        #api_client = ApiClient(access_token=access_token)
        token="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzaWQiOiI5MDUzOTQ6MDU1NDAyMDk4MmRmNjdhYiIsInVpZCI6OTA1Mzk0LCJ3dWlkIjo5OTA0OTE1NiwicGlkIjo2NTcxNywieHBpZCI6MTQxNjg1LCJwdHlwZSI6OCwicyI6MTAzLCJyIjpbMl0sImFkbWluIjpmYWxzZSwiYmwiOmZhbHNlLCJhZG1pbl9yb2xlcyI6bnVsbCwiaXNfcmVmcmVzaCI6ZmFsc2UsInJlZnJlc2hfa2V5IjoiIiwiY291bnRyeSI6IlJVIiwiYXBpZHMiOls2NTcxNyw2ODk5Niw2ODYwMSw2ODQyOCw2ODk3Myw2ODg4Miw2OTAzNCw2ODg2NSw2OTM3Myw2OTM2NSw2ODY1Niw2OTQyNCw2OTMwNyw2ODcxNSw2ODc1OCw2ODg5Nyw2ODg4MSw2OTE4MCw2OTA5Myw2OTQwNiw2ODMzNSw2ODc0Miw2ODE1Miw2OTI2Myw2ODU0NSw2ODUxOCw2ODUwNCw2ODYxOSw2ODQ2MSw2OTAxMyw2OTM0NSw2OTM4Myw2ODUzMSw2ODkwOSw2OTAyOCw2ODcwNiw2OTAyMCw2ODg3MSw2OTQ0NSw2OTMyNSw2ODM4MF0sImVhcGlkcyI6WzE0MTY4NSwxMTA1OTAsMTEwNTcyLDEyOTExNiwyMTg0OTksMTI4MTU1LDEzNTY4NiwxMzUyNDcsMTM3NjQ0LDEyNTczOCwxNDE3ODUsMTQwNTY0LDEyNzM3NCwxNDcwNTIsMzI0NzgyLDExMDQ1MywxMTQ2MTMsMzE3Njg5LDIxNTU5OSw2MTI4LDEzMDI4OCwxMjczOTAsMTM5MDM3LDU0MjYsMTE0NDk1LDEyNjM5OCwyMDg3NjMsMTQwMzUyLDE0NTAzMywxMDU2ODgsMTAxNTQ4LDExMTA1OSwxNDAzNDEsMzEyNzQ1LDEyNjcwNywxMjY2OTgsMzIzNjUzLDEzNDY5NCwxMDg3MjIsMTEyNjg1LDIxODMyMF0sInVzaHMiOlsxMDMsMzJdLCJ2ZXJzaW9uIjoxLCJkZXZpY2VfdXVpZCI6ImJhNzJiNTA5ZjhkMjQxN2E4ODI2OTlmZmRjYWM0ZjIyIiwiZXhwIjoxNzMzODMxNDgyLCJpYXQiOjE3MzI5Njc0ODJ9.JJJtje-KWRub4mWhWK_rs_w6nyBwtIGVJmauTzcKD889Rs4rZ3yh30KRwoMn0az26oseF6Dpdyru3qRNAMMgFOa165p8oLmHbIW6UP37wh-qT6o0oEVbQ1wM2syrp3IQ3U6LanV7HfdByE2hNra3dPYHuSJxexh_aJoDaO5ZPkFHxgYcqe3tETDAiecTkJHVim-sVVbQ9ZFDDbMPM4xDVyzTrWb2fShCdUjCfWJiKxyyU093bdD4CRlqsAHCMyRUa6JcHQ6UyQ0rAZQyCscu4IT8jVmGBTopP9X4f0RyOtb22IDLwBP1Dpoml-orkfX_R-OnGbaz5hQnq_T3ClAM4A"
        api_client = ApiClient(access_token=token)
        start_time = time.time()
        transaction_id = 2106345063
        detail = await api_client.get_transaction_details(transaction_id)
        print("Transaction detail:")
        print(detail)
    except Exception as e:
        print(f"Error fetching transaction detail: {e}")
        return


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
