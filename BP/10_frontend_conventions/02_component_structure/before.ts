// Tema: un componente concentra demasiados detalles de presentación en el mismo archivo.
import { Component } from '@angular/core';

@Component({ selector: 'demo-products-before', standalone: true,
  template: '<h2>Products</h2><ul><li>Coffee</li><li>Tea</li></ul>' })
export class ProductsBeforeComponent {}
