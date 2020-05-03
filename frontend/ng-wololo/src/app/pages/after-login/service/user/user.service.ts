import { Injectable } from "@angular/core";
import { HttpClient, HttpHeaders } from "@angular/common/http";
import { UserDto } from "./model/user-dto";
import { Enviroment } from "../enviroment";

@Injectable({
  providedIn: "root",
})
export class UserService {
  // the actual JWT token
  private _token: string;

  // the token expiration date
  public token_expires: Date;

  // the username of the logged in user
  public username: string;

  // error messages received from the login attempt
  public errors: any = [];

  constructor(public http: HttpClient) {
    this.login();
  }

  // Uses http.post() to get an auth token from djangorestframework-jwt endpoint
  public login(
    user: UserDto = new UserDto("titans55", "titans5562")
  ): Promise<any> {
    return this.http
      .post(
        "http://" + Enviroment.BASE_URL + "/token-auth/",
        JSON.stringify(user),
        this.httpOptions
      )
      .toPromise()
      .then(
        (data) => {
          console.log(data);
          this.updateData(data["token"]);
        },
        (err) => {
          this.errors = err["error"];
        }
      );
  }

  public logout() {
    this._token = null;
    this.token_expires = null;
    this.username = null;
  }

  private updateData(token) {
    this._token = token;
    this.errors = [];

    // decode the token to read the username and expiration timestamp
    const token_parts = this._token.split(/\./);
    const token_decoded = JSON.parse(window.atob(token_parts[1]));
    this.token_expires = new Date(token_decoded.exp * 1000);
    this.username = token_decoded.username;
  }

  // Refreshes the JWT token, to extend the time the user is logged in
  public refreshToken() {
    this.http
      .post(
        "http://" + Enviroment.BASE_URL + "/token-refresh/",
        JSON.stringify({ token: this._token }),
        this.httpOptions
      )
      .subscribe(
        (data) => {
          this.updateData(data["token"]);
        },
        (err) => {
          this.errors = err["error"];
        }
      );
  }

  getToken(): string {
    return this._token;
  }

  private get httpOptions() {
    return {
      headers: new HttpHeaders({
        "Content-Type": "application/json",
      }),
    };
  }
}
