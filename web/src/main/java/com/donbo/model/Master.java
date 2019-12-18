package com.donbo.model;

import com.fasterxml.jackson.annotation.JsonFormat;
import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import javax.persistence.*;
import javax.validation.constraints.NotNull;
import java.time.LocalTime;
import java.util.List;

@Entity
@Table(name = "master")
@Data
@AllArgsConstructor
@NoArgsConstructor
public class Master {

    @Id
    @GeneratedValue(strategy = GenerationType.SEQUENCE)
    @Column(name = "id", nullable = false)
    private Long id;

    @Column(name = "name", nullable = false)
    @NotNull
    private String name;

    @Column(name = "phone_number", nullable = false)
    @NotNull
    private String phoneNumber;

    @Column(name = "start_work_time")
    @JsonFormat(shape= JsonFormat.Shape.STRING, pattern="HH:mm:ss")
    private LocalTime startWorkTime;

    @Column(name = "end_work_time")
    @JsonFormat(shape= JsonFormat.Shape.STRING, pattern="HH:mm:ss")
    private LocalTime endWorkTime;

    @Column(name = "password")
    @NotNull
    private String password;

//    @Column(name = "days")
//    private List<String> workingDays;

    @Column(name = "appointment_duration_minutes")
    private Integer serviceDurationMinutes;

    @Column(name = "email")
    @NotNull
    private String email;

    @OneToMany(mappedBy = "master", cascade = CascadeType.ALL, orphanRemoval = true)
    @JsonIgnore
    private List<Appointment> appointments;
}
