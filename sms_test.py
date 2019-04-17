from twilio.rest import Client

# 下面认证信息的值在你的twilio账户里可以找到
accountSid = "AC4428399695d4fb4048b0e95a2b1fd883"
auth_token = "b2954ae4a7f716b228c30c114d396bbc"

client = Client(accountSid, auth_token)

message = client.messages.create(
    to="+8613761725517",  # 区号+你的手机号码
    from_="+12565810974",  # 你的twilio电话号码
    body="hello")

print(message.sid)
