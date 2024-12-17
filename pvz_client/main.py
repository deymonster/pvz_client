from pvz_client.api_auth import *
from pvz_client.api_client import *
import time
import json
import asyncio


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
        token="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzaWQiOiI5MDUzOTQ6YzNiNzk3NTZkOWIzYmNmZiIsInVpZCI6OTA1Mzk0LCJ3dWlkIjo5OTA0OTE1NiwicGlkIjowLCJ4cGlkIjowLCJwdHlwZSI6MCwicyI6MCwiciI6bnVsbCwiYWRtaW4iOmZhbHNlLCJibCI6ZmFsc2UsImFjIjp0cnVlLCJhZG1pbl9yb2xlcyI6bnVsbCwiaXNfcmVmcmVzaCI6ZmFsc2UsInJlZnJlc2hfa2V5IjoiIiwiY291bnRyeSI6IlJVIiwiYXBpZHMiOm51bGwsImVhcGlkcyI6bnVsbCwiYWxsb3dlZCI6Ikd2K0JBZ0VCQzBGc2JHOTNaV1JNYVhOMEFmK0NBQUgvZ0FBQVFYOERBUUwvZ0FBQkJBRUxVR2xqYTNCdmFXNTBTV1FCQkFBQkRsQnBZMnR3YjJsdWRFVjRkRWxrQVFRQUFRVlRhR0Z5WkFFR0FBRUVVbTlzWlFFR0FBQUEvZ0pwLzRJQUtRSDlBZ0ZxQWYwRVV1b0Jad0VDQUFIOUFocmFBZjRxWkFFZ0FRSUFBZjBDR3dnQi9RTitmZ0VnQVFJQUFmMENHaVFCL1FQNTRBRWdBUUlBQWYwQ0YvSUIvUVJUc2dFZ0FRSUFBZjBDRzFRQi9RUnRFZ0VnQVFJQUFmMENGcGdCL1FhckJnRWdBUUlBQWYwQ0dnSUIvUW14OGdFZ0FRSUFBZjBDSGZvQi9RbmdpZ0VnQVFJQUFmMENHTllCL1FucFhBRWdBUUlBQWYwQ0dTd0IvUU4vYWdFZ0FRSUFBZjBDSGVvQi9RUGQxQUVnQVFJQUFmMENHR0FCL1FQakhBRWdBUUlBQWYwQ0htQUIvUU53V2dFZ0FRSUFBZjBDSFhZQi9RUklhZ0VnQVFJQUFmMENHa0lCL1FQalBBRWdBUUlBQWYwQ0dpSUIvaS9nQVNBQkFnQUIvUUljZUFIOUF4bFlBU0FCQWdBQi9RSWJ5Z0g5QXptd0FTQUJBZ0FCL1FJZVBBSDlBMUZrQVNBQkFnQUIvUUlaREFIOUExN3FBU0FCQWdBQi9RSVYzZ0g5QTEvWUFTQUJBZ0FCL1FJVWNBSDlBMS84QVNBQkFnQUIvUUlkSGdIOUEyT21BU0FCQWdBQi9RSVhnZ0g5QTlaVUFTQUJBZ0FCL1FJYktnSDlBOXQ4QVNBQkFnQUIvUUlkd2dIOUE5M21BU0FCQWdBQi9RSVcyZ0g5QStrMkFTQUJBZ0FCL1FJZURnSDlCQnhNQVNBQkFnQUIvUUlYVEFIOUJDQ2VBU0FCQWdBQi9RSVhNQUg5QkNRTUFTQUJBZ0FCL1FJWFpnSDlCRE5ZQVNBQkFnQUIvUUlhV2dIOUJENDZBU0FCQWdBQi9RSWJTQUg5QkVpQUFTQUJBZ0FCL1FJWUZnSDlCRW9vQVNBQkFnQUIvUUlZeEFIOUJIellBU0FCQWdBQi9RSWJPQUg5Qmw3MkFTQUJBZ0FCL1FJYURnSDlCcFJlQVNBQkFnQUIvUUllaWdIOUJxbWdBU0FCQWdBQi9RSWRtZ0g5Q1l0U0FTQUJBZ0FCL1FJV09BSDlBL0M0QVNBQkFnQT0iLCJ2ZXJzaW9uIjoxLCJkZXZpY2VfdXVpZCI6ImJhNzJiNTA5ZjhkMjQxN2E4ODI2OTlmZmRjYWM0ZjIyIiwiZXhwIjoxNzM0NDUzMTE3LCJpYXQiOjE3MzQzNjY3MTd9.F1KTh-IdcMsLi7UVODPADM_Jfkm798UWgN2DLkhg22w1iirW3CCB2h1a4GqlchLaIJJzdaMR87kjFjBID9DPpTdNs4wbsHS_prLfWDdjBC9Adt-kVtinqyM0As64lsx1K11MfdUGlmQuYIvZJ-v85R3HVgmN-uymuujTgfWKPsu1NgQcDJ_N1YQCRyvwQmInHy10oOPzzCrZJanGMvVTqLC5je2I2kr7dbVvVKOwNotvXgsoP7UATWbIS8VQKUVeE2BDxhD-iNAN1u22TV3TXpNgYrQZu70BlT_qiW1RsFeGLxIVRMyPgMjrNrDt8aSZxb7W_KrZhhGbHSBvGhSPGQ"
        api_client = ApiClient(access_token=token)
        # start_time = time.time()
        # transaction_id = 2111287280
        operations = await api_client.get_operations(date_from="2024-12-15", date_to="2024-12-15")
        print(operations)
        # end_time = time.time()
        # print(f"Time taken: {end_time - start_time} seconds")
        # with open("transaction_details.json", "w", encoding="utf-8") as file:
            # json.dump([operation.model_dump() for operation in operations], file, ensure_ascii=False, indent=4)

        #print("Transaction detail:")
        #print(detail)
        #payments = await api_client.get_partner_payments(pickpoint_id=141685, limit=10, offset=0)
        #print(payments)
        #print(f'Total payments: {len(payments)}')
        #report = await api_client.get_handling_report()
        #report = await api_client.get_handling_report_by_pickpoint(pickpoint_id=127374)
        # report = await api_client.get_detail_good_hadling(pickpoint_id=127374, goods_id=16307356)
        # print(report)
        
        
    except HTTPException as e:
        print(f"HTTP Error: {e.status_code} - {e.message}")
        return
    except Exception as e:
        print(f"Error fetching transaction detail: {e}")
        return


if __name__ == "__main__":
    
    asyncio.run(main())
