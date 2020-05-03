import { Component, OnInit } from "@angular/core";
import { FormBuilder, FormGroup, Validators } from "@angular/forms";
import { UserService } from "src/app/pages/after-login/service/user/user.service";
import { Router } from "@angular/router";

@Component({
  selector: "woo-login-form",
  templateUrl: "./login-form.component.html",
  styleUrls: ["./login-form.component.css"],
})
export class LoginFormComponent implements OnInit {
  isSubmitted: boolean = false;
  loginForm: FormGroup;
  serversideErrors: any;

  countries = ["USA", "Germany", "Italy", "France"];

  requestTypes = ["Claim", "Feedback", "Help Request"];

  constructor(
    formBuilder: FormBuilder,
    private userService: UserService,
    private router: Router
  ) {
    this.loginForm = this.createFormGroupWithBuilder(formBuilder);
  }

  ngOnInit() {}

  createFormGroupWithBuilder(formBuilder: FormBuilder) {
    return formBuilder.group({
      username: ["", Validators.required],
      password: ["", [Validators.required, Validators.minLength(6)]],
    });
  }

  onSubmit() {
    console.log(this.loginForm.value);
    this.isSubmitted = true;
    if (this.loginForm.invalid) {
      return;
    }
    this.userService
      .login(this.loginForm.value)
      .then(() => {
        this.serversideErrors = undefined;
        this.router.navigateByUrl("/game");
      })
      .catch((err) => {
        console.log(err);
        this.serversideErrors = err;
      });
  }
}
