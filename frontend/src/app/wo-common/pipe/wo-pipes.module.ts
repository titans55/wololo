import { NgModule } from "@angular/core";
import { CommonModule } from "@angular/common";
import { HumanizeCamelCasePipe } from "./humanize-camel-case.pipe";

@NgModule({
  imports: [CommonModule],
  declarations: [HumanizeCamelCasePipe],
  exports: [HumanizeCamelCasePipe],
})
export class WoPipesModule {}
