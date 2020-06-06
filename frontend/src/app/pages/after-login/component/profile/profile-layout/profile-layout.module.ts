import { NgModule } from "@angular/core";
import { CommonModule } from "@angular/common";
import { ProfileLayoutComponent } from "./component/profile-layout.component";

@NgModule({
  imports: [CommonModule],
  declarations: [ProfileLayoutComponent],
  exports: [ProfileLayoutComponent],
})
export class ProfileLayoutModule {}
