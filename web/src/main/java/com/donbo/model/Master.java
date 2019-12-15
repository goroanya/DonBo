package com.donbo.model;

import com.fasterxml.jackson.annotation.JsonFormat;

import javax.persistence.*;
import java.time.LocalTime;
import java.util.List;

@Entity
@Table(name = "master")
public class Master {

    @Id
    @GeneratedValue(strategy = GenerationType.SEQUENCE)
    @Column(name = "id", nullable = false)
    private Long id;

    @Column(name = "name", nullable = false)
    private String name;

    @Column(name = "phone_number", nullable = false)
    private String phoneNumber;

    @Column(name = "start_work_time")
    @JsonFormat(shape= JsonFormat.Shape.STRING, pattern="HH:mm:ss")
    private LocalTime startWorkTime;

//    @Column(name = "days")
//    private List<String> workingDays;

    @Column(name = "appointment_duration_minutes")
    private Integer serviceDurationMinutes;

    @Column(name = "email")
    private String email;

    @OneToMany(mappedBy = "master", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<Appointment> appointments;
}
