package com.donbo.controller;

import com.donbo.model.Appointment;
import com.donbo.service.AppointmentService;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping(path = "/appointments", produces = "application/json")
@CrossOrigin(origins="*")
public class AppointmentController {
    private final AppointmentService service;

    public AppointmentController(AppointmentService service) {
        this.service = service;
    }

    @GetMapping
    public List<Appointment> findAll(@RequestParam(name = "masterId", required = false) Long masterId){
        return masterId == null ? service.findAll() : service.findAllByMasterId(masterId);
    }
}
