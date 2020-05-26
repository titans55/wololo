import { NgModule } from "@angular/core";
import { CommonModule } from "@angular/common";
import { RankingComponent } from "./component/ranking.component";
import { WoCommonModule } from "../../../../wo-common/wo-common.module";
import { RouterModule } from "@angular/router";

@NgModule({
  imports: [CommonModule, WoCommonModule, RouterModule],
  declarations: [RankingComponent],
})
export class RankingModule {}
