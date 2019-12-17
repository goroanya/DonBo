package com.donbo.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class PageController {

    @GetMapping("/all_appointments")
    public String allAppointmentsPage(){
        return "allAppointments";
    }

}
