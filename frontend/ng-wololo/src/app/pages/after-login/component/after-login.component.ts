import { Component, OnInit } from "@angular/core";
import { RouterOutletEnum } from "../enum/router-outlet.enum";
import { WebsocketService } from "../service/websocket.service";

@Component({
  selector: "woo-after-login",
  templateUrl: "./after-login.component.html",
})
export class AfterLoginComponent implements OnInit {
  constructor(websocketService: WebsocketService) {
    websocketService.initWebsockets();
  }

  get afterLoginRouterOutlet(): string {
    return RouterOutletEnum.ROUTER_OUTLET_NAME;
  }

  ngOnInit() {}
}
