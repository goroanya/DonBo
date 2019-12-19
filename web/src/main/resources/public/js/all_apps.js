document.addEventListener('DOMContentLoaded', function() {

    // console.log(MY_APP.contextPath);
    // console.log(MY_APP.user);

    var calendarEl = document.getElementById('calendar');
    const id = 1;


    (async () => {

        const rawMaster = fetch(`http://localhost:8080/masters/${id}`);
        const c1 = (await rawMaster).json();
        const master = await c1;

        const rawResponse =
            fetch(`http://localhost:8080/appointments?masterId=${id}`);

        const content = (await rawResponse).json();
        const c = await content;
        console.log(c);

        const ar = c.map(el => {
            let bla = {};
            bla.title = "Клієнт: " + el.client.name + "("+el.client.phoneNumber +")\n" + el.description;
            bla.start = el.date + "T" + el.startTime + ".000";
            return bla;
        });
        console.log(ar);
        //
        // console.log(content);
        console.log(master.serviceDurationMinutes);
        var calendar = new FullCalendar.Calendar(calendarEl, {
            locale: 'ru',
            plugins: [ 'timeGrid','dayGrid' ],
            height: 670,
            header: {
                left: 'dayGridMonth,timeGridWeek,timeGridDay custom1',
                center: 'title',
                right: 'custom2 prevYear,prev,next,nextYear'
            },
//            buttonText: {
//                today:    'Сьогодні',
//                month:    'Місяць',
//                week:     'Тиждень',
//                day:      'День'
//            },
            //monthNames: ['Січень', 'Лютий', 'Березень', 'Квітень', 'Травень', 'Червень', 'Липень',
            //'Серпень', 'Вересень', 'Жовтень', 'Листопад', 'Грудень'],
            //monthNamesShort: ['січ.','лют.','берез.','квіт.','трав.','черв.','лип.','серп.','верес.',
            //'жовт.','листоп.','груд.'],
            minTime: master.startWorkTime,
            maxTime: master.endWorkTime,
            weekends: false,
            events: ar,
            navLinks: true,
            eventLimit: true,
            defaultTimedEventDuration: '00:'+master.serviceDurationMinutes,
                //,
            views: {
                dayGrid: {
                    eventLimit: 3
                },
                timeGrid: {
                    eventLimit: 2
                }
            }
        });

        calendar.render();
    })();

});