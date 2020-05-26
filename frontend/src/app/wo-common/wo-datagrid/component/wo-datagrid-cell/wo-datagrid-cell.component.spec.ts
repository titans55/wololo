/* tslint:disable:no-unused-variable */
import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { By } from '@angular/platform-browser';
import { DebugElement } from '@angular/core';

import { WoDatagridCellComponent } from './wo-datagrid-cell.component';

describe('WoDatagridCellComponent', () => {
  let component: WoDatagridCellComponent;
  let fixture: ComponentFixture<WoDatagridCellComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ WoDatagridCellComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(WoDatagridCellComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
