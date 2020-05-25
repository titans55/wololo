import { NgModule } from "@angular/core";
import { CommonModule } from "@angular/common";
import { RankingComponent } from "./component/ranking.component";
import { WoCommonModule } from "../../../../wo-common/wo-common.module";
import { RankingService } from "./service/ranking.service";

@NgModule({
  imports: [CommonModule, WoCommonModule],
  declarations: [RankingComponent],
  providers: [RankingService],
})
export class RankingModule {}
