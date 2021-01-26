package com.donbo.service;

import com.donbo.model.Appointment;
import com.donbo.repository.AppointmentRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.crossstore.ChangeSetPersister;
import org.springframework.stereotype.Service;

import javax.validation.constraints.NotNull;
import java.util.List;

@Service
public class AppointmentService {

    private final AppointmentRepository repository;

    @Autowired
    public AppointmentService(AppointmentRepository repository) {
        this.repository = repository;
    }

    public List<Appointment> findAll(){
        return repository.findAll();
    }

    public Appointment findById(Long id){
        return repository.findById(id).orElseThrow(RuntimeException::new);
    }

    public List<Appointment> findAllByMasterId(@NotNull Long masterId) {
        List<Appointment> ap = repository.findAppointmentByMasterId(masterId);
        return ap;
    }
}
