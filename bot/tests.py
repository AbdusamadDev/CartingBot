# {
#     "count": 3,
#     "next": None,
#     "previous": None,
#     "results": [
#         {
#             "receiver_phone_number": "+998945555555",
#             "product_count": 44.0,
#             "date_delivery": "2024-01-01T00:23:00+05:00",
#             "product_name": "abani abasi",
#             "product_info": "asdfjkhasdf",
#             "product_type": "kg",
#             "from_location": ["Chust"],
#             "to_location": ["Chust"],
#             "address": "asdfasfdasdfasdf",
#             "status": "active",
#             "id": 5,
#             "client": {
#                 "first_name": None,
#                 "last_name": None,
#                 "obj_status": "available",
#                 "user": {
#                     "phonenumber": "+998945556655",
#                     "user_type": "client",
#                     "first_name": None,
#                     "last_name": None,
#                     "id": 66,
#                 },
#             },
#         },
#         {
#             "receiver_phone_number": "+998901231231",
#             "product_count": 123.0,
#             "date_delivery": "2024-05-03T16:23:00+05:00",
#             "product_name": "123123",
#             "product_info": "123123",
#             "product_type": "m",
#             "from_location": [],
#             "to_location": [],
#             "address": "chust",
#             "status": "active",
#             "id": 2,
#             "client": {
#                 "first_name": "123123",
#                 "last_name": "1",
#                 "obj_status": "available",
#                 "user": {
#                     "phonenumber": "+998200000000",
#                     "user_type": "client",
#                     "first_name": None,
#                     "last_name": None,
#                     "id": 24,
#                 },
#             },
#         },
#         {
#             "receiver_phone_number": "+998940055565",
#             "product_count": 10.0,
#             "date_delivery": "2024-04-19T12:18:18+05:00",
#             "product_name": "banana",
#             "product_info": "asdkfjlhaljkdfsljkasdf",
#             "product_type": "kg",
#             "from_location": [],
#             "to_location": [],
#             "address": "Namangan Region\r\nBogi Eram 8",
#             "status": "active",
#             "id": 1,
#             "client": {
#                 "first_name": "AAAAAAAAAAAAAAAAAAAAAAAAAa",
#                 "last_name": None,
#                 "obj_status": "available",
#                 "user": {
#                     "phonenumber": "+998940055567",
#                     "user_type": "client",
#                     "first_name": None,
#                     "last_name": None,
#                     "id": 2,
#                 },
#             },
#         },
#     ],
# }


# class Solution:
#     def myAtoi(self, s: str) -> int:
#         s = s.strip()
#         symbol = -1
#         if s.startswith("+"):
#             symbol = +1
#         elif s.startswith("-"):
#             symbol = -1
#         else:
#             symbol = +1
#         ranger = lambda integer: (
#             2**31 - 1
#             if integer > 2**31 - 1
#             else -(2**31) if integer < -(2**31) else integer
#         )
#         if s:
#             if s[0] in ["+", "-"]:
#                 s = s[1:]
#         if s.isdigit():
#             return ranger(int(s) * symbol)
#         else:
#             for index, i in enumerate(s):
#                 if not i.isdigit():
#                     if not s[:index]:
#                         return 0
#                     return ranger(int(s[:index]) * symbol)
#         return 0
 