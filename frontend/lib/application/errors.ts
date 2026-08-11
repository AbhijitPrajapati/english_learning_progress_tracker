export class ApplicationError extends Error {
  constructor(message: string, options?: ErrorOptions) {
    super(message, options)
    this.name = "ApplicationError"
  }
}

export class EmailAlreadyRegistered extends ApplicationError {
  constructor() {
    super("Email is already registered")
    this.name = "EmailAlreadyRegistered"
  }
}

export class InvalidCredentials extends ApplicationError {
  constructor() {
    super("Invalid credentials")
    this.name = "InvalidCredentials"
  }
}

export class InvalidToken extends ApplicationError {
  constructor() {
    super("Invalid token")
    this.name = "InvalidToken"
  }
}