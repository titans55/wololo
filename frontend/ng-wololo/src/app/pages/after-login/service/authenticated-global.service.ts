import { Injectable } from "@angular/core";
import { Enviroment } from "./enviroment";
import { HttpClient, HttpHeaders } from "@angular/common/http";

@Injectable({
  providedIn: "root",
})
export class AuthenticatedGlobalService {
  constructor(public http: HttpClient) {}

  private httpOptions() {
    return {
      headers: new HttpHeaders({
        "Content-Type": "application/json",
      }),
    };
  }

  get(url: string): Promise<any> {
    return this.http
      .get("http://" + Enviroment.BASE_URL + "/" + url, this.httpOptions())
      .toPromise();
  }

  post(url: string, data?: any): Promise<any> {
    return this.http
      .post(
        "http://" + Enviroment.BASE_URL + "/" + url,
        data,
        this.httpOptions()
      )
      .toPromise();
  }

  put() {}

  delete() {}
}
