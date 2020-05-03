import { Component, OnInit } from "@angular/core";
import { WebsocketService } from "../service/websocket.service";
import { AfterRouterOutletEnum } from "../enum/after-router-outlet.enum";

@Component({
  selector: "woo-after-login",
  templateUrl: "./after-login.component.html",
})
export class AfterLoginComponent implements OnInit {
  constructor(websocketService: WebsocketService) {
    websocketService.initWebsockets();
  }

  get afterLoginRouterOutlet(): string {
    return AfterRouterOutletEnum.ROUTER_OUTLET_NAME;
  }

  ngOnInit() {}
}
