package com.app.SpringBootRestApp.Controller;

import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.app.SpringBootRestApp.Bean.TestBean;


@CrossOrigin
@RestController
@RequestMapping(path = "/test", produces = "application/json")
public class FrontController {
    
    @GetMapping(path = "/test")
    public TestBean test() {
        TestBean testBean = new TestBean();
        testBean.setText("MiraTest123");
        
        return testBean;
    }
}
