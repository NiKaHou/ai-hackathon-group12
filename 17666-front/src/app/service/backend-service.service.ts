import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class BackendServiceService {

  constructor(private http: HttpClient) { }

  testApi(): Observable<any> {
    const url = `http://localhost:8080/test/test`;
    return this.http.get(url);
  }

  predict(request: any): Observable<any> {
    const url = `http://localhost:5000/predict3`;
    return this.http.post(url,request);
  }
}
