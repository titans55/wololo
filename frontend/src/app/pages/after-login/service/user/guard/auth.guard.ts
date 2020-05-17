// src/app/auth/auth-guard.service.ts
import { Injectable } from "@angular/core";
import { Router, CanActivate } from "@angular/router";
import { UserService } from "../user.service";
@Injectable()
export class AuthGuard implements CanActivate {
  constructor(public userService: UserService, public router: Router) {}
  canActivate(): boolean {
    if (!this.userService.isAuthenticated()) {
      this.router.navigate([""]);
      return false;
    }
    return true;
  }
}
