from jinja2 import Environment, FileSystemLoader
import os
from config import PACKAGE_BASE, OUTPUT_DIR, TEMPLATE_DIR

env = Environment(
    loader=FileSystemLoader(TEMPLATE_DIR), trim_blocks=True, lstrip_blocks=True
)


def prompt_fields():
    """
    Prompt para coleta de campos da entidade.
    Formato: nome:tipo[:length][:positive]

    Tipos suportados: String, Integer, Long, Double, Float, Boolean, LocalDateTime, LocalDate, BigDecimal

    Exemplos:
    - nome:String:100
    - idade:Integer::positive
    - preco:BigDecimal::positive
    - ativo:Boolean
    """
    fields = []
    print("\n--- Configuração de Campos ---")
    print("Formatos aceitos:")
    print("  nome:String:100")
    print("  idade:Integer::positive")
    print("  preco:BigDecimal::positive")
    print("  percentual:Double::positive")
    print("  ativo:Boolean")
    print("  nascimento:LocalDate")
    print()

    while True:
        entry = input(
            "Campo (nome:tipo[:length][:positive]) ou ENTER para terminar: "
        ).strip()
        if entry == "":
            break

        parts = entry.split(":")
        if len(parts) < 2:
            print("❌ Erro: você precisa digitar pelo menos nome e tipo")
            print("   Exemplo: nome:String")
            continue

        field_name = parts[0].strip()
        field_type = parts[1].strip()

        # Validate field type
        valid_types = [
            "String",
            "Integer",
            "Long",
            "Double",
            "Float",
            "Boolean",
            "LocalDateTime",
            "LocalDate",
            "UUID",
            "BigDecimal",
        ]
        if field_type not in valid_types:
            print(
                f"❌ Erro: tipo '{field_type}' não suportado. Use: {', '.join(valid_types)}"
            )
            continue

        field = {
            "name": field_name,
            "type": field_type,
            "length": (
                int(parts[2]) if len(parts) > 2 and parts[2].strip().isdigit() else None
            ),
            "not_null": True,
            "positive": (
                True
                if len(parts) > 3 and parts[3].strip().lower() == "positive"
                else False
            ),
        }

        fields.append(field)
        print(f"✅ Adicionado: {field_name} ({field_type})")

    return fields


def prompt_relationships():
    """
    Prompt para coleta de relacionamentos entre entidades.
    Formato: nome:tipo:target[:mapped_by][:options]

    Tipos suportados: OneToMany, ManyToOne, OneToOne, ManyToMany
    Options: cascade, not_null, owner, inverse_field

    Exemplos:
    - pedidos:OneToMany:Pedido:cliente:cascade
    - categoria:ManyToOne:Categoria::not_null
    - endereco:OneToOne:Endereco::cascade,owner
    - tags:ManyToMany:Tag::cascade,inverse_field=posts
    """
    relationships = []
    print("\n--- Configuração de Relacionamentos ---")
    print("Formatos aceitos:")
    print("  OneToMany: pedidos:OneToMany:Pedido:cliente:cascade")
    print("  ManyToOne: categoria:ManyToOne:Categoria::not_null")
    print("  OneToOne:  endereco:OneToOne:Endereco::cascade,owner")
    print("  ManyToMany: tags:ManyToMany:Tag::cascade,inverse_field=posts")
    print("\nOpções: cascade, not_null, owner, inverse_field=nome")
    print()

    while True:
        entry = input(
            "Relacionamento (nome:tipo:target[:mapped_by][:options]) ou ENTER para terminar: "
        ).strip()
        if entry == "":
            break

        parts = entry.split(":")
        if len(parts) < 3:
            print("❌ Erro: formato mínimo é nome:tipo:target")
            print("   Exemplo: pedidos:OneToMany:Pedido")
            continue

        rel_name = parts[0].strip()
        rel_type = parts[1].strip()
        rel_target = parts[2].strip()

        # Validate relationship type
        valid_types = ["OneToMany", "ManyToOne", "OneToOne", "ManyToMany"]
        if rel_type not in valid_types:
            print(
                f"❌ Erro: tipo '{rel_type}' não suportado. Use: {', '.join(valid_types)}"
            )
            continue

        # Parse mapped_by
        mapped_by = parts[3].strip() if len(parts) > 3 and parts[3].strip() else None

        # Parse options
        options = {}
        if len(parts) > 4 and parts[4].strip():
            option_parts = [opt.strip() for opt in parts[4].split(",")]
            for opt in option_parts:
                if "=" in opt:
                    key, value = opt.split("=", 1)
                    options[key.strip()] = value.strip()
                else:
                    options[opt] = True

        relationship = {
            "name": rel_name,
            "type": rel_type,
            "target": rel_target,
            "mapped_by": mapped_by,
            "cascade": options.get("cascade", False),
            "not_null": options.get("not_null", False),
            "owner": options.get("owner", False),
            "inverse_field": options.get("inverse_field", None),
        }

        relationships.append(relationship)
        print(f"✅ Adicionado: {rel_name} ({rel_type} -> {rel_target})")

    return relationships


def render_template(template_name, context, output_path):
    template = env.get_template(template_name)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(template.render(context))
    print(f"Gerado: {output_path}")


def main():
    print("╔══════════════════════════════════════╗")
    print("║           GGV-AUTO-CRUD              ║")
    print("║     Gerador de CRUD com JPA          ║")
    print("╚══════════════════════════════════════╝")
    print()

    entity_name = input("📝 Nome da entidade (Ex: Cliente): ").strip()
    if not entity_name:
        print("❌ Nome da entidade é obrigatório!")
        return

    table_name = input(f"🗃️  Nome da tabela (padrão: {entity_name.lower()}): ").strip()
    if not table_name:
        table_name = entity_name.lower()

    print(f"\n🏗️  Configurando entidade: {entity_name}")
    print(f"📋 Tabela: {table_name}")

    fields = prompt_fields()
    relationships = prompt_relationships()

    if not fields and not relationships:
        print("❌ Erro: nenhum campo ou relacionamento informado.")
        return

    print(f"\n📋 Resumo da entidade {entity_name}:")
    print(f"   Tabela: {table_name}")
    print(f"   Campos: {len(fields)}")
    print(f"   Relacionamentos: {len(relationships)}")

    # Show summary
    if fields:
        print("\n   📝 Campos:")
        for field in fields:
            column_name = field["name"].upper()
            print(
                f"      - {field['name']}: {field['type']} → Coluna: {column_name}"
                + (f" (max: {field['length']})" if field.get("length") else "")
                + (" [positivo]" if field.get("positive") else "")
            )

    if relationships:
        print("\n   🔗 Relacionamentos:")
        for rel in relationships:
            print(
                f"      - {rel['name']}: {rel['type']} -> {rel['target']}"
                + (f" (mapped by: {rel['mapped_by']})" if rel.get("mapped_by") else "")
                + (" [cascade]" if rel.get("cascade") else "")
                + (" [not null]" if rel.get("not_null") else "")
            )

    confirm = input(f"\n✅ Confirma a geração dos arquivos? (s/N): ").strip().lower()
    if confirm not in ["s", "sim", "y", "yes"]:
        print("❌ Operação cancelada.")
        return

    context = {
        "entity_name": entity_name,
        "table_name": table_name,
        "package_base": PACKAGE_BASE,
        "fields": fields,
        "relationships": relationships,
    }

    templates = [
        ("entity.java.j2", f"{OUTPUT_DIR}/{entity_name}/{entity_name}.java"),
        (
            "repository.java.j2",
            f"{OUTPUT_DIR}/{entity_name}/{entity_name}Repository.java",
        ),
        ("request.java.j2", f"{OUTPUT_DIR}/{entity_name}/{entity_name}Request.java"),
        ("response.java.j2", f"{OUTPUT_DIR}/{entity_name}/{entity_name}Response.java"),
        ("mapper.java.j2", f"{OUTPUT_DIR}/{entity_name}/{entity_name}Mapper.java"),
        ("service.java.j2", f"{OUTPUT_DIR}/{entity_name}/{entity_name}Service.java"),
        (
            "controller.java.j2",
            f"{OUTPUT_DIR}/{entity_name}/{entity_name}Controller.java",
        ),
        (
            "service_test.java.j2",
            f"{OUTPUT_DIR}/{entity_name}/{entity_name}ServiceTest.java",
        ),
        (
            "controller_test.java.j2",
            f"{OUTPUT_DIR}/{entity_name}/{entity_name}ControllerTest.java",
        ),
    ]

    print(f"\n🚀 Gerando arquivos para {entity_name}...")

    for template_name, output_path in templates:
        try:
            render_template(template_name, context, output_path)
        except Exception as e:
            print(f"❌ Erro ao gerar {output_path}: {e}")
            return

    print(
        f"\n🎉 Todos os arquivos foram gerados com sucesso em: {OUTPUT_DIR}/{entity_name}/"
    )
    print("\n📂 Arquivos gerados:")
    for _, output_path in templates:
        print(f"   ✓ {output_path}")


if __name__ == "__main__":
    main()
