import { Component, OnInit } from "@angular/core";
import { WebsocketService } from "../service/websocket/websocket.service";
import { AfterRouterOutletEnum } from "../enum/after-router-outlet.enum";
import { VillageResourcesService } from "../partials/component/village-resources/service/village-resources.service";

@Component({
  selector: "woo-after-login",
  templateUrl: "./after-login.component.html",
})
export class AfterLoginComponent implements OnInit {
  constructor(
    private websocketService: WebsocketService,
    private villageResourcesService: VillageResourcesService
  ) {
    villageResourcesService.production(true).then(() => {
      websocketService.initWebsockets(true);
    });
  }

  get afterLoginRouterOutlet(): string {
    return AfterRouterOutletEnum.ROUTER_OUTLET_NAME;
  }

  ngOnInit() {}
}
