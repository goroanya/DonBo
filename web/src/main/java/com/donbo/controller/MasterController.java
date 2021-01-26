package com.donbo.controller;

import com.donbo.model.Appointment;
import com.donbo.model.Master;
import com.donbo.service.MasterService;
import org.springframework.web.bind.annotation.*;

import javax.validation.Valid;
import java.util.List;

@RestController
@RequestMapping("/masters")
public class MasterController {

    private final MasterService service;

    public MasterController(MasterService service) {
        this.service = service;
    }

    @GetMapping
    public List<Master> findAll(){
        return service.findAll();
    }

    @PostMapping
    public Master save(@RequestBody @Valid Master master){
        return service.save(master);
    }

    @GetMapping("/{id}")
    public Master findById(@PathVariable(name = "id") Long id){
        return service.findById(id);
    }
}
