import graphene
from graphene_django import DjangoObjectType

from superheroes.models import Superheroe, Vote
from users.schema import UserType
from graphql import GraphQLError


class SuperheroeType(DjangoObjectType):
    class Meta:
        model = Superheroe


class VoteType(DjangoObjectType):
    class Meta:
        model = Vote

class Query(graphene.ObjectType):
    superheroe = graphene.List(SuperheroeType)
    votes = graphene.List(VoteType)

    def resolve_superheroe(self, info, **kwargs):
        return Superheroe.objects.all()

    def resolve_votes(self, info, **kwargs):
        return Vote.objects.all()

class CreateSuperheroe(graphene.Mutation):
    id = graphene.Int()
    name = graphene.String()
    image = graphene.String()
    characteristics=graphene.String()
    posted_by = graphene.Field(UserType)

    class Arguments:
        name = graphene.String()
        image = graphene.String()
        characteristics=graphene.String()
        
        
    def mutate(self, info, name,image,characteristics):
        user = info.context.user or None

        superheroe = Superheroe( 
                    name=name, 
                    image=image,
                    characteristics=characteristics,
                    posted_by = user,
                   )
        superheroe.save()

        return CreateSuperheroe(
            id=superheroe.id,
            name=superheroe.name,
            image=superheroe.image,
            characteristics=superheroe.characteristics,
            posted_by=superheroe.posted_by,
        )


# Add the CreateVote mutation

class CreateVote(graphene.Mutation):
    user = graphene.Field(UserType)
    superheroe = graphene.Field(SuperheroeType)

    class Arguments:
        superheroe_id = graphene.Int()

    def mutate(self, info, superheroe_id):
        user = info.context.user
        if user.is_anonymous:
            #raise Exception('You must be logged to vote!')
            raise GraphQLError('GraphQLError: You must be logged to vote!')


        superheroe = Superheroe.objects.filter(id=superheroe_id).first()
        if not superheroe:
            raise Exception('Invalid superheroe!')

        Vote.objects.create(
            user=user,
            superheroe=superheroe,
        )

        return CreateVote(user=user, superheroe=superheroe)




class Mutation(graphene.ObjectType):
    create_superheroe = CreateSuperheroe.Field()
    create_vote = CreateVote.Field()
