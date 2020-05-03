import { Injectable } from "@angular/core";
import { Enviroment } from "./enviroment";
import { HttpClient, HttpHeaders } from "@angular/common/http";
import { UserService } from "./user/user.service";

@Injectable({
  providedIn: "root",
})
export class AuthenticatedGlobalService {
  private token: string;
  constructor(public http: HttpClient, private userService: UserService) {
    this.token = userService.getToken();
  }

  private httpOptions() {
    return {
      headers: new HttpHeaders({
        "Content-Type": "application/json",
        // Authorization: "JWT " + this.token,
      }),
    };
  }

  get(url: string): Promise<any> {
    if (true) {
      return this.http
        .get("http://" + Enviroment.BASE_URL + "/" + url, this.httpOptions())
        .toPromise();
    } else {
      return Promise.reject("token missing");
    }
  }

  post(url: string, data?: any): Promise<any> {
    if (true) {
      return this.http
        .post(
          "http://" + Enviroment.BASE_URL + "/" + url,
          data,
          this.httpOptions()
        )
        .toPromise();
    } else {
      return Promise.reject("token missing");
    }
  }

  put() {}

  delete() {}
}
