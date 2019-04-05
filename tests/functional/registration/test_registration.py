from __future__ import unicode_literals
import pytest
from textx import (metamodel_from_str,
                   clear_language_registrations, clear_generator_registrations,
                   register_language, register_generator,
                   language_description, generator_description,
                   language_for_file, languages_for_file,
                   metamodel_for_language, metamodel_for_file,
                   LanguageDesc, GeneratorDesc, TextXRegistrationError)
from textx.metamodel import TextXMetaModel


def mymetamodel_callable():
    return metamodel_from_str('MyModel: INT;')


def generator_callable():
    pass


@pytest.fixture
def language_registered():
    clear_language_registrations()
    register_language('test-lang',
                      pattern='*.test',
                      description='test-lang description',
                      metamodel=mymetamodel_callable)


def test_register_language():
    """
    Test both style of language registration.
    """
    clear_language_registrations()
    register_language('test-lang',
                      pattern='*.test',
                      description='test-lang description',
                      metamodel=mymetamodel_callable)

    language = language_description('test-lang')

    assert type(language) is LanguageDesc
    assert language.name == 'test-lang'
    assert language.pattern == '*.test'
    assert language.description == 'test-lang description'
    assert language.metamodel == mymetamodel_callable

    clear_language_registrations()
    register_language(LanguageDesc('test-lang',
                                   pattern='*.test',
                                   description='test-lang description',
                                   metamodel=mymetamodel_callable))

    language = language_description('test-lang')

    assert type(language) is LanguageDesc
    assert language.name == 'test-lang'
    assert language.pattern == '*.test'
    assert language.description == 'test-lang description'
    assert language.metamodel == mymetamodel_callable


def test_asking_for_unregistered_language_raises_error():
    """
    """
    with pytest.raises(TextXRegistrationError, match='.*not registered.*'):
        language_description('unexisting')


def test_register_already_existing_language():
    """
    Test that trying to register a language with the name already registered
    will raise `TextXRegistrationError`.
    """

    clear_language_registrations()
    register_language('test-lang',
                      pattern='*.test',
                      description='test-lang description',
                      metamodel=mymetamodel_callable)

    with pytest.raises(TextXRegistrationError, match='.*already registered.*'):
        register_language('test-lang',
                          pattern='*.test',
                          description='test-lang description',
                          metamodel=mymetamodel_callable)


def test_declaratively_registered_languages_always_available():
    """
    Declaratively registered languages will be re-registered at the first API
    call. textX language is declaratively registered and thus is always
    accessible.
    """
    clear_language_registrations()
    tx_lang = language_description('textx')

    assert tx_lang.name == 'textX'
    assert tx_lang.pattern == '*.tx'


def test_language_for_file():
    """
    Test providing language description for a given file name or pattern.
    """

    clear_language_registrations()
    tx_lang = language_description('textx')

    assert tx_lang is language_for_file('test.tx')
    assert tx_lang is language_for_file('*.tx')


def test_metamodel_for_language(language_registered):
    """
    Test finding a meta-model for the given language name.
    """

    mm = metamodel_for_language('test-lang')
    assert isinstance(mm, TextXMetaModel)


def test_metamodel_for_file(language_registered):
    """
    Test finding a meta-model for the given file or file pattern.
    """
    mm = metamodel_for_file('mymodel.test')
    assert isinstance(mm, TextXMetaModel)

    mm = metamodel_for_file('*.test')
    assert isinstance(mm, TextXMetaModel)

    mm = metamodel_for_file('somefile*.test')
    assert isinstance(mm, TextXMetaModel)


def test_multiple_languages_for_the_same_pattern():
    """
    If multiple languages are registered for the same file pattern
    `language_for_file` shall raise `TextXRegistrationError`.
    """
    clear_language_registrations()
    register_language('test-lang',
                      pattern='*.test',
                      description='test-lang description',
                      metamodel=mymetamodel_callable)
    register_language('test-lang2',
                      pattern='*.test',
                      description='test-lang2 description',
                      metamodel=mymetamodel_callable)

    with pytest.raises(TextXRegistrationError,
                       match='Multiple languages can parse.*'):
        language_for_file('Somefile.test')

    assert len(languages_for_file('Somefile.test')) == 2


def test_file_without_any_language():
    """
    Test that asking for a language for a file or file pattern for which
    no languages are registered will raise an error.
    """

    with pytest.raises(TextXRegistrationError,
                       match='No language registered that can parse.*'):
        language_for_file('Somefile.nolang')


def test_metamodel_callable_must_return_a_metamodel():
    """
    Test that meta-model callable must return an instance of TextXMetaModel.
    """

    def invalid_metamodel_callable():
        return 42

    clear_language_registrations()
    register_language('test-lang',
                      pattern='*.test',
                      description='test-lang description',
                      metamodel=invalid_metamodel_callable)

    with pytest.raises(TextXRegistrationError,
                       match='.*Meta-model type for language.*'):
        metamodel_for_language('test-lang')


def test_register_generator():
    """
    Test both style of generator registration.
    """

    clear_generator_registrations()
    register_generator('test-lang',
                       target='Java',
                       description='test-lang Java generator',
                       generator=generator_callable)

    generator = generator_description('test-lang', 'java')

    assert type(generator) is GeneratorDesc
    assert generator.language == 'test-lang'
    assert generator.target == 'Java'
    assert generator.description == 'test-lang Java generator'
    assert generator.generator == generator_callable

    clear_generator_registrations()
    register_generator(GeneratorDesc('test-lang',
                                     target='Java',
                                     description='test-lang Java generator',
                                     generator=generator_callable))

    generator = generator_description('test-lang', 'java')

    assert type(generator) is GeneratorDesc
    assert generator.language == 'test-lang'
    assert generator.target == 'Java'
    assert generator.description == 'test-lang Java generator'
    assert generator.generator == generator_callable


def test_asking_for_unregistered_generator_raises_error():
    """
    Test searching for unexisting generator raises an error.
    """
    with pytest.raises(TextXRegistrationError, match='.*No generators.*'):
        generator_description('flow-dsl', 'unexisting_target')

    with pytest.raises(TextXRegistrationError, match='.*No generators.*'):
        generator_description('unexisting_language', 'unexisting_target')


def test_register_already_existing_generator():
    """
    Test that trying to register a generator with the language name and target
    already registered will raise `TextXRegistrationError`.
    """

    clear_generator_registrations()
    register_generator('test-lang',
                       target='Java',
                       description='test-lang Java generator',
                       generator=generator_callable)

    with pytest.raises(TextXRegistrationError, match='.*already registered.*'):
        register_generator('test-lang',
                           target='Java',
                           description='test-lang Java generator',
                           generator=generator_callable)


def test_declaratively_registered_generator_always_available():
    """
    Declaratively registered generators will be re-registered at the first API
    call.
    """
    clear_generator_registrations()
    generator = generator_description('flow-dsl', 'plantuml')

    assert generator.language == 'flow-dsl'
    assert generator.target == 'PlantUML'
    assert callable(generator.generator)
