import telebot

# التوكن الخاص بك جاهز هنا
TOKEN = '8917798144:AAG49jtagcX6f6_LDsLgMX5WDcEKS-DxfYg'
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def moderate_chat(message):
  try:
    # التحقق من وجود روابط في الرسالة
    if message.text and (
        'http://' in message.text
        or 'https://' in message.text
        or 't.me/' in message.text
    ):

      # التحقق من صلاحيات المرسل (تخطي المشرفين)
      chat_member = bot.get_chat_member(message.chat.id, message.from_user.id)
      if chat_member.status in ['creator', 'administrator']:
        return

      # حذف رسالة الرابط
      bot.delete_message(message.chat.id, message.message_id)

      # كتم المستخدم لمدة 20 دقيقة (1200 ثانية)
      bot.restrict_chat_member(
          message.chat.id,
          message.from_user.id,
          until_date=message.date + 1200,
          can_send_messages=False,
      )

      # إرسال تنبيه بالمخالفة
      warning = bot.send_message(
          message.chat.id,
          f'عذراً @{message.from_user.username or message.from_user.first_name},'
          ' ممنوع إرسال الروابط هنا! تم كتمك لمدة 20 دقيقة.',
      )

      # حذف رسالة التحذير تلقائياً بعد 10 ثوانٍ لعدم إزعاج المجموعة
      import time

      time.sleep(10)
      bot.delete_message(message.chat.id, warning.message_id)

  except Exception as e:
    print(f'حدث خطأ: {e}')


print('Bot is running...')
bot.infinity_polling()
