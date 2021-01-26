package com.donbo.controller;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class PageController {

    @GetMapping("/")
    public String home(Model model){
        model.addAttribute("module","index");
        return "index";
    }

    @GetMapping("/all_appointments")
    public String allAppointmentsPage(Model model){
        model.addAttribute("module", "all_appointments");
        return "allAppointments";
    }

    @GetMapping("/login")
    public String login(Model model){
        model.addAttribute("module", "login");
        return "login";
    }

    @GetMapping("/register")
    public String register(Model model){
        model.addAttribute("model","register");
        return "register";
    }

    @GetMapping("/schedule")
    public String schedule(){
        return "schedule";
    }


}
