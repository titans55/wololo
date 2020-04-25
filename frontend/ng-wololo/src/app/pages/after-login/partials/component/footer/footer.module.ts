import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FooterComponent } from './component/footer.component';

@NgModule({
  imports: [
    CommonModule
  ],
  exports: [FooterComponent],
  declarations: [FooterComponent]
})
export class FooterModule { }
