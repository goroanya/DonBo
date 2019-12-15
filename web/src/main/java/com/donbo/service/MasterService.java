package com.donbo.service;

import com.donbo.model.Master;
import com.donbo.repository.MasterRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class MasterService {

    private final MasterRepository repository;

    @Autowired
    public MasterService(MasterRepository repository) {
        this.repository = repository;
    }

    public List<Master> findAll(){
        return repository.findAll();
    }

    public Master findById(Long id){
        return repository.findById(id).orElseThrow(RuntimeException::new);
    }
}
