// Tema: el nombre identifica la pantalla y el selector evita colisiones genéricas.
import { Component } from '@angular/core';

@Component({
  selector: 'demo-product-list',
  standalone: true,
  template: '<p>Products</p>',
})
export class ProductListComponent {}
