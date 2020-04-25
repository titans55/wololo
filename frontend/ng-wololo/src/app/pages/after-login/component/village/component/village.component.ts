import { Component, OnInit } from "@angular/core";
import { VillageService } from "../service/village.service";

@Component({
  selector: "woo-village",
  templateUrl: "./village.component.html",
  styleUrls: ["./village.component.css"],
})
export class VillageComponent implements OnInit {
  buildingsConfig;
  constructor(service: VillageService) {
    this.buildingsConfig = service.buildingsConfig;
  }

  ngOnInit() {}
}
