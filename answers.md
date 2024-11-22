# Answers to the questions posted in the challenge

## 1. Why can we not easily split this project into two microservices?
The items and users are closely related on the DB level: CartItem from "user" namespace has a foreign key
to the Item from "item" namespace.
Normally, different microservices should use separate databases.

Also the user usecase uses the item repository directly.

A split into two microservices is possible, but would be awkward and inefficient.
It could be done by:
- making the CartItem hold an opaque Item ID instead of a foreign key
- adding an item usecase to the user/cart service, that would call out to the item service to check for item IDs
- making the user usecase use that new item usecase

## 2. Why does this project not adhere to the clean architecture even though we have seperate modules for api, repositories, usecases and the model?
1. Usecases (lower layer) depend on schema objects (higher layer), because they use them as function parameters.
  Dependencies should only go towards lower layers.
  Here, the usecases are dependent on an object from a higher layer.

  To solve this, the "api" layer should create DTO objects from the schema object, and then pass that to the usecases.
  DTOs are from a layer below usecases.

  Personally, I find that this is not a big deal.
  DTOs that would be created from the schema objects and passed to the usecases would have the most probably always
  be equal. In my FastAPI projects I was passing the schema objects to usecases.

2. Usecases (lower layer) return schema objects (higher layer).
  Usecases should return entities.

3. Usecases raise HTTP exceptions. These belong to the interface layer above.
  Usecases should raise their own Exceptions that then get resolved to HTTP exceptions in the interface layers.

4. Usecases use a DB connection directly instead of using a repository,
  in which the DB connection can be abstracted out.

5. Usecases create DB models and pass them on to repositories.
  In "pure" clean architecture, entities or DTO should be passed to adapters/repositories.

  Having said that, I use SQL Alchemy models as entities.
  They can be created as in-memory objects without a DB connection, which makes them easy to use in usecase unit tests.
  Though it can be harder to keep it only in memory with more complicated foreign key relationships.

6. User usecase uses item repository directly instead of going through an item usecase.

7. Repository/adapter layer isn't abstracted out. Usecases depend on a specific repository implementation.

## 3. What would be your plan to refactor the project to stick to the clean architecture?
1. Refactor usecases and repositories into classes that get created with FastAPI depends mechanism.
   Usecases would depend on an abstract repository.
   A specific implementation would get injected with the FastAPI `Depends` mechanism.
   The chosen implementation might depend on the configuration.

   See the code changes I've made TODO.

2. Isolate a Cart usecase from the User usecase. Move the `add_item_to_cart` there.

3. Item usecase gets a `get_single` method, that will be used by Cart usecase.

4. Have usecases return SQL Alchemy models, which will be acting as entities.
   Pydantic schemas can be created from these automatically, and returned from the API level.
   That still keeps the external interface independent from the internal data structures.
   If the interface would stray far enough from the DB models, custom functions for translation of model to schema
   object would need to be introduced.

5. Have usecases raise custom exceptions, that return SQL Alchemy models, which will be acting as entities.

## 4. How can you make dependencies between modules more explicit?
1. Show dependencies in the models with imports and not using bare strings in the foreign keys.

2. Don't split the code vertically into "user" and "item".
   Instead have directories for the layers.
   Then the models could be visibly closely related in a single file or directory.

3. Have three usecases - Cart, Item, User. Item and User are independent, Cart depends on Item and User.

# Stretch goals
* Fork the repository and start refactoring - DONE, see [here](https://github.com/butla/be-task-ca)
* Write meaningful tests (TODO add notes)
  - functional one going through everything
  - add item to cart, wrong item or user ID
  - pure usecase unit test example
* Replace the SQL repository with an in-memory implementation
  - use depends with a config objects
