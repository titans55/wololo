import { Injectable } from "@angular/core";
import { HttpClient, HttpHeaders } from "@angular/common/http";
import { UserDto } from "./model/user-dto";
import { Enviroment } from "../enviroment";
import { ReplaySubject, BehaviorSubject } from "rxjs";
import * as moment from "moment";
import { Router } from "@angular/router";

@Injectable({
  providedIn: "root",
})
export class UserService {
  // the actual JWT token
  get token(): string {
    return localStorage.getItem("token");
  }

  // the token expiration date
  public expires_at: Date;

  // the username of the logged in user
  public username: string;

  // error messages received from the login attempt

  constructor(public http: HttpClient, private router: Router) {}

  // Uses http.post() to get an auth token from djangorestframework-jwt endpoint
  public login(user: UserDto): Promise<any> {
    return this.http
      .post(
        "http://" + Enviroment.BASE_URL + "/token-auth/",
        JSON.stringify(user),
        this.httpOptions
      )
      .toPromise()
      .then((data) => {
        console.log(data);
        this.updateData(data["token"]);
      })
      .catch((err) => {
        return Promise.reject(err["error"]);
      });
  }

  public logout() {
    this.expires_at = null;
    this.username = null;
    localStorage.removeItem("token");
    localStorage.removeItem("expires_at");
    this.router.navigateByUrl("/");
  }

  private updateData(token) {
    localStorage.setItem("token", token);

    // decode the token to read the username and expiration timestamp
    const token_parts = this.token.split(/\./);
    const token_decoded = JSON.parse(window.atob(token_parts[1]));
    this.expires_at = new Date(token_decoded.exp * 1000);
    this.username = token_decoded.username;
  }

  public isAuthenticated(): boolean {
    return (
      localStorage.getItem("token") != null ||
      (this.expires_at != null && moment().isBefore(this.expires_at))
    );
  }

  // Refreshes the JWT token, to extend the time the user is logged in
  public refreshToken() {
    this.http
      .post(
        "http://" + Enviroment.BASE_URL + "/token-refresh/",
        JSON.stringify({ token: this.token }),
        this.httpOptions
      )
      .toPromise()
      .then((data) => {
        this.updateData(data["token"]);
      })
      .catch((err) => {
        console.log(err);
      });
  }

  private get httpOptions() {
    return {
      headers: new HttpHeaders({
        "Content-Type": "application/json",
      }),
    };
  }
}
