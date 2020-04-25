import { Component, OnInit } from "@angular/core";
import { AfterLoginRoutesEnum } from "src/app/pages/after-login/after-login.routing";

@Component({
  selector: "woo-navbar",
  templateUrl: "./navbar.component.html",
  styleUrls: ["./navbar.component.css"],
})
export class NavbarComponent implements OnInit {
  isCollapsed: boolean = true;

  constructor() {}

  ngOnInit() {}

  get AfterLoginRoutesEnum() {
    return AfterLoginRoutesEnum;
  }
}
