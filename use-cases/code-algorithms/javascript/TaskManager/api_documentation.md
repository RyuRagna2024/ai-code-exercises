# Product Catalog API Documentation

This document contains the complete technical specification, OpenAPI definition, and developer usage guide for the Product Catalog API.

---

## 1. API Endpoint Reference

### Endpoint Overview
- **HTTP Method:** `GET`
- **Path:** `/api/products`
- **Purpose:** Retrieve a paginated list of product records from the database with flexible filtering (by category, price range, and stock availability) and customizable field sorting.

### Authentication
- **Requirements:** None (Public Endpoint).

### Query Parameters

| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `category` | String | No | None | Filter products by category slug or name (exact match). |
| `minPrice` | Number | No | None | Filter for products with price greater than or equal to `minPrice`. |
| `maxPrice` | Number | No | None | Filter for products with price less than or equal to `maxPrice`. |
| `sort` | String | No | `createdAt` | Field name to sort results by (e.g., `price`, `createdAt`). |
| `order` | String | No | `desc` | Sort direction: `asc` (ascending) or `desc` (descending). |
| `page` | Integer | No | `1` | Page number for pagination (must be 1 or greater). |
| `limit` | Integer | No | `20` | Number of items to return per page. |
| `inStock` | Boolean | No | None | When string `'true'`, filters for products where `stockQuantity > 0`. |

---

### Response Format & Status Codes

#### 200 OK — Success Response
Returns a JSON object containing an array of `products` and a `pagination` metadata block.

```json
{
  "products": [
    {
      "_id": "61fa9bcf5c130b2e6d675432",
      "name": "Wireless Headphones",
      "description": "High-quality wireless headphones with noise cancellation",
      "price": 89.99,
      "category": "electronics",
      "stockQuantity": 45,
      "createdAt": "2023-02-01T15:32:47Z",
      "updatedAt": "2023-03-15T09:21:08Z"
    }
  ],
  "pagination": {
    "total": 42,
    "page": 1,
    "limit": 20,
    "pages": 3
  }
}

### 500 Internal Server Error — Failure Response
- Triggered when an unhandled database driver error or unexpected server exception occurs.

{
  "error": "Server error",
  "message": "Failed to fetch products"
}

## 2. OpenAPI 3.0 Specification (YAML)

openapi: 3.0.0
info:
  title: Products API
  description: API for querying, filtering, and retrieving product inventory.
  version: 1.0.0
servers:
  - url: [https://api.example.com](https://api.example.com)
    description: Production Server

paths:
  /api/products:
    get:
      summary: List Products
      description: Get a list of products with flexible filtering, sorting, and pagination options.
      operationId: listProducts
      parameters:
        - name: category
          in: query
          required: false
          schema:
            type: string
          description: Filter products by category exact match.
        - name: minPrice
          in: query
          required: false
          schema:
            type: number
            format: float
          description: Minimum price filter ($gte).
        - name: maxPrice
          in: query
          required: false
          schema:
            type: number
            format: float
          description: Maximum price filter ($lte).
        - name: sort
          in: query
          required: false
          schema:
            type: string
            default: createdAt
          description: Model field to sort results by.
        - name: order
          in: query
          required: false
          schema:
            type: string
            enum: [asc, desc]
            default: desc
          description: Sort ordering direction.
        - name: page
          in: query
          required: false
          schema:
            type: integer
            default: 1
            minimum: 1
          description: Page number offset.
        - name: limit
          in: query
          required: false
          schema:
            type: integer
            default: 20
            minimum: 1
            maximum: 100
          description: Number of product records per page.
        - name: inStock
          in: query
          required: false
          schema:
            type: boolean
          description: Set to true to filter products with stockQuantity > 0.
      responses:
        '200':
          description: Successfully retrieved list of products.
          content:
            application/json:
              schema:
                type: object
                properties:
                  products:
                    type: array
                    items:
                      $ref: '#/components/schemas/Product'
                  pagination:
                    $ref: '#/components/schemas/Pagination'
        '500':
          description: Internal Server Error.
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErrorResponse'

components:
  schemas:
    Product:
      type: object
      required:
        - _id
        - name
        - price
        - category
        - stockQuantity
      properties:
        _id:
          type: string
          example: 61fa9bcf5c130b2e6d675432
        name:
          type: string
          example: Wireless Headphones
        description:
          type: string
          example: High-quality noise-canceling headphones
        price:
          type: number
          format: float
          example: 89.99
        category:
          type: string
          example: electronics
        stockQuantity:
          type: integer
          example: 45
        createdAt:
          type: string
          format: date-time
          example: 2023-02-01T15:32:47Z
        updatedAt:
          type: string
          format: date-time
          example: 2023-03-15T09:21:08Z

    Pagination:
      type: object
      properties:
        total:
          type: integer
          example: 42
        page:
          type: integer
          example: 1
        limit:
          type: integer
          example: 20
        pages:
          type: integer
          example: 3

    ErrorResponse:
      type: object
      properties:
        error:
          type: string
          example: Server error
        message:
          type: string
          example: Failed to fetch products

---

## 3. Developer Usage Guide

### Integration Guide: Fetching Products with Node.js & Axios
**Target Audience:** Junior Web Developers  
**Tone:** Friendly, practical, and beginner-focused

Welcome! This guide explains how to consume the Product Catalog API endpoint using JavaScript.

#### 1. Authentication
Public product retrieval (`GET /api/products`) requires **no API keys or Bearer tokens**. You can query this endpoint directly.

#### 2. How to Request Data
When querying the API, pass parameters in the URL query string to filter results:

```javascript
const axios = require('axios');

const API_URL = '[https://api.example.com/api/products](https://api.example.com/api/products)';

async function getProducts() {
  try {
    const response = await axios.get(API_URL, {
      params: {
        category: 'electronics',
        maxPrice: 100,
        page: 1,
        limit: 10
      }
    });

    console.log('Products found:', response.data.products);
    console.log('Pagination info:', response.data.pagination);
  } catch (error) {
    console.error('Error fetching products:', error.message);
  }
}

