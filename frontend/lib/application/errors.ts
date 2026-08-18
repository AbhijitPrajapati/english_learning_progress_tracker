export class ApplicationError extends Error {
  constructor(message: string, options?: ErrorOptions) {
    super(message, options);
    this.name = "ApplicationError";
  }
}

export class EmailAlreadyRegistered extends ApplicationError {
  constructor() {
    super("Email is already registered");
    this.name = "EmailAlreadyRegistered";
  }
}

export class InvalidCredentials extends ApplicationError {
  constructor() {
    super("Invalid credentials");
    this.name = "InvalidCredentials";
  }
}

export class InvalidCurrentPassword extends ApplicationError {
  constructor() {
    super("Current password is incorrect");
    this.name = "InvalidCurrentPassword";
  }
}

export class InvalidToken extends ApplicationError {
  constructor() {
    super("Invalid token");
    this.name = "InvalidToken";
  }
}

export class SpeechNotFound extends ApplicationError {
  constructor() {
    super("Speech not found");
    this.name = "SpeechNotFound";
  }
}

export class InvalidAudio extends ApplicationError {
  constructor(message = "Invalid audio upload") {
    super(message);
    this.name = "InvalidAudio";
  }
}

export class RequestRejected extends ApplicationError {
  constructor(message: string, options?: ErrorOptions) {
    super(message, options);
    this.name = "RequestRejected";
  }
}

export class QuotaReached extends ApplicationError {
  constructor() {
    super("Analysis quota reached.");
    this.name = "QuotaReached";
  }
}
