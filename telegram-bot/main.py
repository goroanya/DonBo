from time import sleep
from datetime import date, timedelta
from threading import Thread

from sqlalchemy import or_, and_

from bot import bot, Appointment
from model import Session

session = Session()

TIME_DELAY_SEC = 10  # test delay


def check_updates():
    while True:
        today_date = date.today()
        appointments = session.query(Appointment) \
            .filter(or_(Appointment.date == today_date, Appointment.date == today_date + timedelta(days=1))) \
            .filter(Appointment.notified == False)
        for app in appointments:
            appointment_date = app.date.strftime("%d.%m.%Y (%A)")
            appointment_start = app.start_time.strftime('%H:%M')
            bot.send_message(app.client_id, f'Підходить час вашого візиту #{app.id}\n' + \
                             f'Дата: {appointment_date}\nЧас: {appointment_start}' + \
                             f"\nТип послуги: {app.description if app.description else 'Не вказано'}\n")
            app.notified = True
        session.commit()

        sleep(TIME_DELAY_SEC)


if __name__ == '__main__':
    Thread(target=check_updates).start()
    bot.polling()
