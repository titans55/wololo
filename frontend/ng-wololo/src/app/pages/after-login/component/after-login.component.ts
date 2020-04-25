import { Component, OnInit } from '@angular/core';
import { RouterOutletEnum } from '../enum/router-outlet.enum';

@Component({
  selector: 'woo-after-login',
  templateUrl: './after-login.component.html',
})
export class AfterLoginComponent implements OnInit {

  constructor() { }

  get afterLoginRouterOutlet(): string{
    return RouterOutletEnum.ROUTER_OUTLET_NAME
  }

  ngOnInit() {
  }

}
