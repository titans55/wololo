import { Component, OnInit } from "@angular/core";
import { AfterLoginRoutesEnum } from "src/app/pages/after-login/after-login.routing";
import { UserService } from "src/app/pages/after-login/service/user/user.service";

@Component({
  selector: "woo-navbar",
  templateUrl: "./navbar.component.html",
  styleUrls: ["./navbar.component.css"],
})
export class NavbarComponent implements OnInit {
  isCollapsed: boolean = true;
  username: string;

  constructor(private userService: UserService) {
    this.username = this.userService.username;
  }

  logout() {
    this.userService.logout();
  }

  ngOnInit() {}

  get AfterLoginRoutesEnum() {
    return AfterLoginRoutesEnum;
  }
}
