package com.donbo.service;

import com.donbo.model.Client;
import com.donbo.repository.ClientRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import javax.validation.constraints.NotNull;
import java.util.List;

@Service
public class ClientService {

    private final ClientRepository repository;

    @Autowired
    public ClientService(ClientRepository repository) {
        this.repository = repository;
    }

    public List<Client> findAll(){
        return repository.findAll();
    }

    public Client findById(Long id){
        return repository.findById(id).orElseThrow(RuntimeException::new);
    }

    public Client save(@NotNull Client client){
        return repository.save(client);
    }
}
