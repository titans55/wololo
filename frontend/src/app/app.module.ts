import { BrowserModule } from "@angular/platform-browser";
import { NgModule } from "@angular/core";

import { AppRoutingModule } from "./app-routing.module";
import { AppComponent } from "./app.component";
import { BrowserAnimationsModule } from "@angular/platform-browser/animations";
import { NgbModule } from "@ng-bootstrap/ng-bootstrap";
import { FormsModule } from "@angular/forms";
import { MapSceneService } from "./pages/after-login/component/map/service/map-scene.service";
import { HttpClientModule } from "@angular/common/http";
import { ToastrModule } from "ngx-toastr";

@NgModule({
  declarations: [AppComponent],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    ToastrModule.forRoot(),
    FormsModule,
    HttpClientModule,
  ],
  exports: [],
  providers: [MapSceneService],
  bootstrap: [AppComponent],
})
export class AppModule {}
