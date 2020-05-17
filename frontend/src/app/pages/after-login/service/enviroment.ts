import { isDevMode } from "@angular/core";

enum EnviromentHostEnum {
  DEV = "localhost:8000/",
  PROD = "",
}

export namespace Enviroment {
  export const HOST: string = isDevMode()
    ? EnviromentHostEnum.DEV
    : EnviromentHostEnum.PROD;
  export const BASE_URL: string = HOST + "api";
  export const BASE_REST_URL: string = HOST + "api/v1";
}
