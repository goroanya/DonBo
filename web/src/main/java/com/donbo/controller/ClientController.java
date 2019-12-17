package com.donbo.controller;

import com.donbo.model.Client;
import com.donbo.service.ClientService;
import org.springframework.web.bind.annotation.*;

import javax.validation.Valid;
import java.util.List;

@RestController
@RequestMapping("/clients")
public class ClientController {

    private final ClientService service;

    public ClientController(ClientService service) {
        this.service = service;
    }

    @GetMapping
    public List<Client> findAllClients(){
        return service.findAll();
    }

    @GetMapping("/{id}")
    public Client findById(@PathVariable("id") Long id){
        return service.findById(id);
    }

    @PostMapping
    public Client saveClient(@RequestBody Client client){
        return service.save(client);
    }
}
