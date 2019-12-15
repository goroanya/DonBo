package com.donbo.model;

import com.fasterxml.jackson.annotation.JsonFormat;

import javax.persistence.*;
import java.time.LocalDate;
import java.time.LocalTime;

@Entity
@Table(name="appointment")
public class Appointment {

    @Id
    @GeneratedValue(strategy = GenerationType.SEQUENCE)
    @Column(name = "id", nullable = false)
    private Long id;

    @Column(name = "start_time", nullable = false)
    @JsonFormat(shape= JsonFormat.Shape.STRING, pattern="HH:mm:ss")
    private LocalTime startTime;

    @Column(name = "date", nullable = false)
    @JsonFormat(shape= JsonFormat.Shape.STRING, pattern="HH:mm:ss")
    private LocalDate date;

    @Column(name="description", nullable = false)
    private String description;

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "client_id", nullable = false)
    private Client client;

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "master_id", nullable = false)
    private Master master;
}
