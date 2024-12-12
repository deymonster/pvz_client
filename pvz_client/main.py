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
        token="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzaWQiOiI5MDUzOTQ6OTU0MzRmOTk2YjZmMWVjYSIsInVpZCI6OTA1Mzk0LCJ3dWlkIjo5OTA0OTE1NiwicGlkIjo2NTcxNywieHBpZCI6MTQxNjg1LCJwdHlwZSI6OCwicyI6MTAzLCJyIjpbMl0sImFkbWluIjpmYWxzZSwiYmwiOmZhbHNlLCJhZG1pbl9yb2xlcyI6bnVsbCwiaXNfcmVmcmVzaCI6ZmFsc2UsInJlZnJlc2hfa2V5IjoiIiwiY291bnRyeSI6IlJVIiwiYXBpZHMiOls2ODQ2MSw2ODcxNSw2OTM2NSw2ODY1Niw2OTQyNCw2NTcxNyw2ODk5Niw2ODYwMSw2ODk3Myw2ODg4Miw2OTAzNCw2ODQyOCw2ODg2NSw2OTM3Myw2ODc1OCw2OTMwNyw2ODg5Nyw2ODc0Miw2ODg4MSw2OTE4MCw2OTA5Myw2OTQwNiw2ODMzNSw2OTI2Myw2ODE1Miw2OTAxMyw2OTM0NSw2ODU0NSw2OTM4Myw2ODUzMSw2ODkwOSw2OTAyOCw2ODcwNiw2ODUxOCw2ODUwNCw2ODYxOSw2OTAyMCw2ODg3MSw2OTQ0NSw2OTMyNSw2ODM4MF0sImVhcGlkcyI6WzE0MTY4NSwxMTA1OTAsMTEwNTcyLDEyOTExNiwyMTg0OTksMTI4MTU1LDEzNTY4NiwxMzUyNDcsMTM3NjQ0LDEyNTczOCwxNDE3ODUsMTQwNTY0LDEyNzM3NCwxNDcwNTIsMzI0NzgyLDExMDQ1MywxMTQ2MTMsMzE3Njg5LDIxNTU5OSw2MTI4LDEzMDI4OCwxMjczOTAsMTM5MDM3LDU0MjYsMTE0NDk1LDEyNjM5OCwyMDg3NjMsMTQwMzUyLDE0NTAzMywxMDU2ODgsMTAxNTQ4LDExMTA1OSwxNDAzNDEsMzEyNzQ1LDEyNjcwNywxMjY2OTgsMzIzNjUzLDEzNDY5NCwxMDg3MjIsMTEyNjg1LDIxODMyMF0sInVzaHMiOlsxMDMsMzJdLCJ2ZXJzaW9uIjoxLCJkZXZpY2VfdXVpZCI6ImJhNzJiNTA5ZjhkMjQxN2E4ODI2OTlmZmRjYWM0ZjIyIiwiZXhwIjoxNzM0Nzk2NTE3LCJpYXQiOjE3MzM5MzI1MTd9.IZhWR3uEmP12eqBR6frUeSI1iPMyMHRPWWdMgw9w6Yul8wlh8Xsl2MU8QmTJiwvrTXdR49WedzOv18O4_V574wM6qknB7uVeRBAdGGElWC3RmG-Sp__8asTZ8OBkAizg-7UeKyQJttfRS-Jfj4gTHpeaxm2h_bZjihKipAc1KsS-1c3BMwfByetPQdJQfbgCVVqj7jRvh7L1ivk5xzQV9YDQrj1HuG18SRsrPFyWVzpU6FVek0G4wx-ypoNsVPtwP4tmvyArns_rJVSTXLQ1WbmdfY3ENtUZgQL8h8xYP7AVnE0i_bCbmzlFbg1Poe5Bklt1yorlH68Iev5fweMcfA"
        api_client = ApiClient(access_token=token)
        # start_time = time.time()
        # transaction_id = 2111287280
        # operations = await api_client.get_operations(date_from="2024-12-1", date_to="2024-12-1")
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
        report = await api_client.get_detail_good_hadling(pickpoint_id=127374, goods_id=16307356)
        print(report)
        
        
    except HTTPException as e:
        print(f"HTTP Error: {e.status_code} - {e.message}")
        return
    except Exception as e:
        print(f"Error fetching transaction detail: {e}")
        return


if __name__ == "__main__":
    
    asyncio.run(main())
